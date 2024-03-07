//
//  ServiceProtocol.swift
//

import Foundation
import CoreBluetooth

protocol ServiceProtocol {
    // Property
    var cacheLifetime: TimeInterval { get set }
    // Read-only property
    var cachedDataSize: Float { get }

    // Simple function
    func refresh()
    // Property between functions
    var cachedDataMaxSize: Double { get set }

    // Function with parameters
    func uploadData(_ data: Data, progressBlock: (Progress) -> Void) async

    // Function with parameters and response
    func requestData(id: String, progressBlock: (Progress) -> Void) async throws -> Data

    // Generic function with parameters and response
    func parseData<Data: Codable, Response>() async throws -> Response where Response : Codable

    // Multiple line function
    func registerDevices<T>(
        deviceA: CBUUID,
        // Internal comment test
        deviceB: CBUUID,
        deviceC: CBUUID
    ) async -> T where T : DeviceListProtocol

    func requestConfig<T>(_ block: @escaping (T) -> Void) async throws -> [String: String]
    func requestConfigParser(_ name: (String, count: Int)) async -> (([String: String]) -> Config)
}

protocol StorageProtocol {
    // Different property type
    func setDeviceID(_ id: String)
    func setDeviceID(_ id: Int)
    func setDeviceID(with id: UUID)
    // func_name: setDeviceIDIntClosure
    func setDeviceID(with id: () -> Int)
    func setDeviceID<T>(_ id: T.Type)

    // Different parameters count and types
    func saveDeviceInfo(fileName: String)
    func saveDeviceInfo(fileName: String, filePath: String)
    func saveDeviceInfo(fileName: String, filePath: Path)
    func saveDeviceInfo(fileName: String, filePath: String, fileExtension: String)
}
